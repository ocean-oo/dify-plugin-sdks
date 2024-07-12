from collections.abc import Generator
from typing import Any
import uuid

from dify_plugin.core.runtime.abstract.request import AbstractRequestInterface
from dify_plugin.core.runtime.entities.dify import ToolProviderType
from dify_plugin.core.runtime.entities.invocation import InvokeType
from dify_plugin.core.runtime.entities.model import LLMResultChunk, RerankResult, TextEmbeddingResult
from dify_plugin.core.runtime.entities.workflow import KnowledgeRetrievalNodeData, NodeResponse, ParameterExtractorNodeData, QuestionClassifierNodeData
from dify_plugin.tool.entities import ToolInvokeMessage
from dify_plugin.utils.io_writer import PluginOutputStream

class RequestInterface(AbstractRequestInterface):
    session_id: str

    def __init__(self, session_id: str) -> None:
        self.session_id = session_id

    def _generate_request_id(self):
        return uuid.uuid4().hex

    def invoke_tool(self, provider_type: ToolProviderType, provider: str, tool_name: str,
                    parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke tool
        """
        request_id = self._generate_request_id()

        PluginOutputStream.session_message(
            session_id=self.session_id, 
            data=PluginOutputStream.stream_invoke_object(data={
                'type': InvokeType.Tool.value,
                'request_id': request_id,
                'request': {
                    'provider_type': provider_type.value,
                    'provider': provider,
                    'tool': tool_name,
                    'parameters': parameters
                }
            }).to_dict()
        )

        yield ToolInvokeMessage(
            type=ToolInvokeMessage.MessageType.TEXT,
            message=ToolInvokeMessage.TextMessage(text='123')
        )

    def invoke_builtin_tool(self, provider: str, tool_name: str, parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke builtin tool
        """
        return super().invoke_builtin_tool(provider, tool_name, parameters)

    def invoke_workflow_tool(self, provider: str, tool_name: str, parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke workflow tool
        """
        return super().invoke_workflow_tool(provider, tool_name, parameters)

    def invoke_api_tool(self, provider: str, tool_name: str, parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke api tool
        """
        return super().invoke_api_tool(provider, tool_name, parameters)

    def invoke_llm(self, provider: str, model_name: str, parameters: dict[str, Any]) -> Generator[LLMResultChunk, None, None]:
        """
        Invoke llm
        """
        return super().invoke_llm(provider, model_name, parameters)

    def invoke_text_embedding(self, provider: str, model_name: str, parameters: dict[str, Any]) -> TextEmbeddingResult:
        """
        Invoke text embedding
        """
        return super().invoke_text_embedding(provider, model_name, parameters)

    def invoke_rerank(self, provider: str, model_name: str, parameters: dict[str, Any]) -> RerankResult:
        """
        Invoke rerank
        """
        return super().invoke_rerank(provider, model_name, parameters)

    def invoke_question_classifier(self, node_data: QuestionClassifierNodeData, inputs: dict) -> NodeResponse:
        """
        Invoke question classifier
        """
        return super().invoke_question_classifier(node_data, inputs)

    def invoke_parameter_extractor(self, node_data: ParameterExtractorNodeData, inputs: dict) -> NodeResponse:
        """
        Invoke parameter extractor
        """
        return super().invoke_parameter_extractor(node_data, inputs)

    def invoke_knowledge_retrieval(self, node_data: KnowledgeRetrievalNodeData, inputs: dict) -> NodeResponse:
        """
        Invoke knowledge retrieval
        """
        return super().invoke_knowledge_retrieval(node_data, inputs)