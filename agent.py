import os
from decouple import config
from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

class MailClassification(BaseModel):
    is_intervention: bool = Field(description="True si c'est une demande d'intervention, False sinon")
    raison: str = Field(description="Justification courte de la classification")


class AgentMail:
    def __init__(self, template:str):
        # add OPENAI_API_KEY
        os.environ["OPENAI_API_KEY"] = config("OPENAI_API_KEY")

        self.prompt = ChatPromptTemplate.from_template(template)
        self.model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.parser = PydanticOutputParser(pydantic_object=MailClassification)

    def classifyMail(self, mail_content: str) -> dict:
        formatted_prompt = self.prompt.format(mail_content=mail_content)
        response = self.model.predict(formatted_prompt)
        return self.parser.parse(response)