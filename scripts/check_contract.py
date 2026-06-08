from agent.schemas.chat import ChatRequest, ChatResponse


def main() -> None:
    request_schema = ChatRequest.model_json_schema()
    response_schema = ChatResponse.model_json_schema()
    print("ChatRequest fields:", sorted(request_schema["properties"].keys()))
    print("ChatResponse fields:", sorted(response_schema["properties"].keys()))


if __name__ == "__main__":
    main()

