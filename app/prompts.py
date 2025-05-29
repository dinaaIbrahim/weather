
from langchain.prompts import PromptTemplate

country_extraction_prompt = PromptTemplate.from_template("""
Extract only the name of the country mentioned in the following query, following these strict rules:
1. If the query explicitly mentions a country, return that country name
2. If only a city is mentioned:
   - Return the most well-known/popular country for that city
   - For example: "Paris" → "France", "London" → "United Kingdom"
3. If no country or recognizable city is mentioned, return "None" and ONLY "None"
4. If no country or recognizable city is mentioned, return "None" with no additional text or punctuation                                                       
5. Return ONLY the country name with no additional text or punctuation
6. If multiple countries are mentioned, return the first one
7. Absolutely never return anything other than a country name or "None"

Examples:
Query: Weather in Cairo
Country: Egypt

Query: Events in Springfield
Country: United States

Query: Hotels in Toronto
Country: Canada

Query: What's the weather today?
Country: None

Query: What should I wear today?
Country: None                                                         
                                                         
Query: {query}
Country:""")


regen_query_prompt = PromptTemplate.from_template("""
Create an enhanced query that combines:
1. The original user query (keep completely unchanged)
2. The exact weather details (include all provided data)
3. The country name (mention clearly in the output)
4. A natural weather description when conditions are: cloudy, windy, snowy, rainy, or sunny

Format exactly like this:
"[Original query exactly as written] [Country: <country>] [Weather data exactly as provided] (Feels [natural description])"

Rules:
- ALWAYS preserve the original query exactly
- ALWAYS include all weather data exactly as provided
- ALWAYS include the country name
- ONLY add description () for: cloudy, windy, snowy, rainy, or sunny conditions
- Description should be 3–5 natural words (e.g., "chilly and damp", "hot and humid")

Examples:
Original: "What should I wear today?"
Country: Canada
Weather: temperature=12°C, clouds=90%, wind=15km/h
Enhanced: "What should I wear today? Country: Canada temperature=12°C, clouds=90%, wind=15km/h (Feels chilly and breezy)"

Original query: {query}
Country: {country}
Weather data:
{weather_details}

Enhanced query:
""")


gen_prompt = PromptTemplate.from_template("""
You are a helpful assistant. Use ONLY the information explicitly provided in the context and rewritten query. Do NOT invent, assume, or add any external details. Be strictly factual and grounded in the data.

Context:
{context}

Rewritten_Query:
{rewritten_query}

Instructions:
- Describe the weather using only terms and information present in the context.
- Suggest suitable activities ONLY if directly supported or clearly implied by the context.
- Recommend clothing choices strictly based on the provided weather details—no guessing or creative additions.

Requirements:
- Provide a clear and coherent final answer.
- Address all three points: (1) weather description, (2) suitable activities, (3) appropriate clothing.
- Stay aligned with the original question's intent.
- Maintain clarity and readability while adhering 100% to the data in context.
""")
