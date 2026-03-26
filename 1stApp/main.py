import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
#from langchain.chains import LLMChain

load_dotenv() # loads the environmental variable  from .env file 


def main():
    #print(f"{os.getenv('OPENAI_API_KEY')}")
    print("Hello from 1stapp!")

    information = """
    Srinivasa Ramanujan Iyengar[a] FRS (22 December 1887 – 26 April 1920) was an Indian mathematician who worked during the early 20th century. Despite having almost no formal training in pure mathematics, he made substantial contributions to mathematical analysis, number theory, infinite series, and continued fractions, including solutions to mathematical problems then considered unsolvable.

    Ramanujan initially developed his own mathematical research in isolation. According to Hans Eysenck, "he tried to interest the leading professional mathematicians in his work, but failed for the most part. What he had to show them was too novel, too unfamiliar, and additionally presented in unusual ways; they could not be bothered."[1] Seeking mathematicians who could better understand his work, in 1913 he began a mail correspondence with the English mathematician G. H. Hardy at the University of Cambridge. Recognising Ramanujan's work as extraordinary, Hardy arranged for him to travel to Cambridge. In his notes, Hardy commented that Ramanujan had produced groundbreaking new theorems, including some that "defeated me completely; I had never seen anything in the least like them before",[2] and some recently proven but highly advanced results.

    Throughout his life, Ramanujan independently compiled nearly 3,900 results (mostly identities and equations).[3] Many were completely novel; his original and highly unconventional results, such as the Ramanujan prime, the Ramanujan theta function, partition formulae and mock theta functions, have opened entire new areas of work and inspired further research.[4] Of his thousands of results, most have been proven correct.[5] The Ramanujan Journal, a scientific journal, was established to publish work in all areas of mathematics influenced by Ramanujan,[6] and his notebooks—containing summaries of his published and unpublished results—have been analysed and studied for decades since his death as a source of new mathematical ideas. As late as 2012, researchers continued to discover that mere comments in his writings about "simple properties" and "similar outputs" for certain findings were themselves profound and subtle number theory results that remained unsuspected until nearly a century after his death.[7][8] He became one of the youngest Fellows of the Royal Society and only the second Indian member, and the first Indian to be elected a Fellow of Trinity College, Cambridge.

    In 1919, ill health—now believed to have been hepatic amoebiasis (a complication from episodes of dysentery many years previously)—compelled Ramanujan's return to India, where he died in 1920 at the age of 32. His last letters to Hardy, written in January 1920, show that he was still continuing to produce new mathematical ideas and theorems. His "lost notebook", containing discoveries from the last year of his life, caused great excitement among mathematicians when it was rediscovered in 1976. 
    """

    summary_template = """
    You are a helpful assistant that can summarize {information} about a person I want you to create:
    1. A short summary.
    2. Two interesting facts about this person.
    """
    summary_prompt_template = PromptTemplate( # A list Contains the key's 
        input_variables=["information"],
        template=summary_template
    )
    # A tempurate of 0.7 means the model will be 30% creative and 70% deterministic
    # Result value near to 1.0 means the model will be more creative
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3) # This llm variable calling the LLM 

    # LCEL  (Langchain Expression Language)
    '''
        LECL Syntax we create a chain nby composing two components a prompt template and a LLM
        IN the below case 
        ------------------
        The information into a prompt string which will eventually be propagated to the LLM  
        And the llm Variable is a Chat open AI object, which takes an input a prompt string 
        and generates text . 

        Now this pipe(|) operator in an expression language is going to create a new runnable chain. 
        By Connecting the output of the left component as an input to the right components ß. 
    '''
    chain = summary_prompt_template | llm # Runnable invoke 
    response = chain.invoke(input={"information": information})
    print(response)
    '''
    # Create a chain
    summary_chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    
    # Run the chain
    result = summary_chain.run(information=information)
    
    print(result)
    '''

    
if __name__ == "__main__":
    main()
