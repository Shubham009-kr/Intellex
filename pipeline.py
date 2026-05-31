from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain
import time
import httpx

def run_research_pipeline(topic: str) -> dict:
    state = {}

    # search agent working
    print("\n" +  "="*50)
    print("step 1: searching the web for relevant information...")
    print("="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages":[("user", f"Find recent, reliable and detailed information on the topic:{topic}")]
    })

    state['search_results'] = search_result['messages'][-1].content

    print("\n search results:", state["search_results"])

    # step 2: reader agent working
    print("\n" +  "="*50)
    print("step 2: reading and analyzing the retrieved information...")
    print("="*50)

    reader_agent = build_reader_agent()
    reader_result =  reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}"
        )]
    })

    state['scraped_content'] = reader_result['messages'][-1].content

    print("\nscraped content: \n", state['scraped_content'])

    #step 3 - writer chain 

    print("\n"+"="*50)
    print("step 3 - Writer is drafting the report ...")
    print("="*50)

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic" : topic,
        "research" : research_combined
    })

    print("\n Final Report\n",state['report'])

    #critic report 

    print("\n"+" ="*50)
    print("step 4 - critic is reviewing the report ")
    print("="*50)

    # Call the critic with retries and a graceful fallback if the model
    # service returns a 429 (capacity exhausted) or other HTTP errors.
    max_retries = 3
    backoff = 2
    feedback = None

    for attempt in range(1, max_retries + 1):
        try:
            feedback = critic_chain.invoke({"report": state['report']})
            break
        except httpx.HTTPStatusError as e:
            status = None
            try:
                status = e.response.status_code
            except Exception:
                pass

            if status == 429:
                print(f"Service capacity exceeded (429). Attempt {attempt}/{max_retries}.")
                if attempt < max_retries:
                    time.sleep(backoff)
                    backoff *= 2
                    continue
                else:
                    feedback = {
                        "error": "Service tier capacity exceeded for the model (429). Try again later or switch to another model/service."}
            else:
                feedback = {"error": f"HTTP error while calling model: {e}"}
            break
        except Exception as e:
            feedback = {"error": f"Unexpected error while calling critic: {e}"}
            break

    state["feedback"] = feedback
    print("\n critic report \n", state['feedback'])

    return state



if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipeline(topic)