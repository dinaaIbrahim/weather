from .config import llm, setup_rag
from .prompts import country_extraction_prompt,regen_query_prompt,gen_prompt
from operator import itemgetter
from .utils import strict_country_validation


# --- Country Detection ---
coun_chain = country_extraction_prompt | llm

def detect_country_llm(query: str) -> str:
    result = coun_chain.invoke({"query": query})
    return strict_country_validation(result.content)


# --- Query Regeneration ---
def regenerate_query(query, weather_details, country):

    regen_chain = regen_query_prompt | llm
    
    return regen_chain.invoke({
        "query": query,
        "weather_details": weather_details,
        "country": country
    }).content.strip()


# --- Final Response Generation ---
retriever = setup_rag()

def generate_final_response(rewritten_query):
    chain = (
        {
            "context": itemgetter("rewritten_query") | retriever,
            "rewritten_query": itemgetter("rewritten_query")
        }
        | gen_prompt
        | llm
    )

    return chain.invoke({"rewritten_query": rewritten_query}).content