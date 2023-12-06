import logging
from typing import List

from eidos import agent_os
from eidos.cpu.call_context import CallContext
from eidos.cpu.llm_message import LLMMessage
from eidos.cpu.memory_unit import MemoryUnit, MemoryUnitConfig
from eidos.system.reference_model import Specable


class ConversationalMemoryUnit(MemoryUnit, Specable[MemoryUnitConfig]):
    async def writeMessages(self, call_context: CallContext, messages: List[LLMMessage]):
        conversationItems = [{
            "process_id": call_context.process_id,
            "thread_id": call_context.thread_id,
            "message": message.model_dump()} for message in messages]

        logging.debug(str(messages))
        logging.debug(conversationItems)

        await agent_os.symbolic_memory.insert("conversation_memory", conversationItems)

    async def getConversationHistory(self, call_context: CallContext) -> List[LLMMessage]:
        existingMessages = []
        async for message in agent_os.symbolic_memory.find("conversation_memory", {
            "process_id": call_context.process_id,
            "thread_id": call_context.thread_id
        }):
            existingMessages.append(LLMMessage.from_dict(message["message"]))

        logging.debug("existingMessages = " + str(existingMessages))
        return existingMessages