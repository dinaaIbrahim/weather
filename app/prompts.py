
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


Examples:
Original: "What should I wear today?"
Country: Canada
Weather: temperature=12°C, clouds=90%, wind=15km/h
Enhanced: "What should I wear today? Country: Canada temperature=12°C, clouds=90%, wind=15km/h (Cloudy and Windy)"

Original query: {query}
Country: {country}
Weather data:
{weather_details}

Enhanced query:
""")


gen_prompt = PromptTemplate.from_template("""
You are a helpful assistant that gives weather-based suggestions using only the data explicitly provided in the context and rewritten query. Do not invent, assume, or include any external knowledge.

**Context:**  
{context}

**Rewritten_Query:**  
{rewritten_query}

### Instructions:  
1. **Weather Description:**  
   - Describe the current weather by including ALL data points provided in the context (temperature, humidity, wind, cloud cover, etc.) without summarization.  
   - Present every relevant metric exactly as given, ensuring no detail is left out.  
   - Based on the given metrics, classify the overall weather into ONE of the following categories: cloudy, windy, snowy, rainy, or sunny.  
     Use these rules for classification:  
       • Cloudy: if cloud cover is high (e.g., >70%).  
       • Windy: if wind speed is strong (e.g., >15 km/h).  
       • Snowy: if temperature is at or below freezing (≤0°C) and precipitation indicates snow (if available).  
       • Rainy: if precipitation indicates rain or if weather context implies rain.  
       • Sunny: if cloud cover is low (e.g., <30%) and no precipitation or strong wind is present.  
     Choose the category that best fits the conditions; if multiple apply, prioritize in this order: snowy, rainy, windy, cloudy, sunny.

2. **Suggested Activities:**  
   - Recommend only activities that are directly supported or clearly implied by the full set of weather details in the context.  
   - Use every piece of provided information to justify or refine the suggestions—no assumptions or external knowledge allowed.

3. **Clothing Recommendations:**  
   - Suggest clothing strictly based on ALL available weather data.  
   - Consider every relevant metric (temperature, humidity, wind, cloud cover) when advising what to wear.  
   - Do not generalize, infer, or add any details beyond what is explicitly present or logically implied by the context.

### Requirements:
- make sure that no information about the weather is left out .    
- Structure your answer clearly using bullet points or short paragraphs for each section.  
- If the context doesn’t have certain information, just leave it out—don’t say it’s missing.
- When making activity or clothing recommendations, base your suggestions on the country as a whole rather than focusing on specific cities
- Make activity and clothing recommendations based on the weather classification (cloudy, windy, snowy, rainy, or sunny) determined from the weather data.                                         
                                          
""")
