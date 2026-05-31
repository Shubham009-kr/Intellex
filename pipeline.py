from agents import build_search_agent, build_reader_agent, writer_Chain, critic_chain

def run_search_pipeline(topic: str) -> dict:
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