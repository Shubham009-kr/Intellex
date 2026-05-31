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

    state["search_results"] = search_result['messages'][-1].content

    print("\n search results:", state["search_results"])