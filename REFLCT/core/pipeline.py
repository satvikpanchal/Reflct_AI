from datetime import datetime
from core.reflection import analyze_feelings
from tools.vision import take_screenshot

class Pipeline:
    def __init__(self, memory_manager):
        self.memory = memory_manager

    def handle_request(self, transcript, user="Satvik"):
        # Check if user wants to store something
        should_store = any(kw in transcript for kw in ["remember", "memorize", "save memory"])
        
        screenshot = take_screenshot() if any(
            w in transcript for w in ["screen", "desktop", "window"]
        ) else None

        # 1. Query memory **only if it's not a memory-saving command**
        past_context = self.memory.query(transcript) if not should_store else None

        # Build memory context for LLM
        memory_context = ""
        if past_context and past_context.get("documents"):
            top_docs = [doc for docs in past_context["documents"] for doc in docs][:3]
            if top_docs:
                print("\n📜 MEMORY CONTEXT:", top_docs, "\n")
                memory_context = "\n".join([f"- {d}" for d in top_docs])

        # Augment transcript with memory for reasoning
        augmented_transcript = transcript
        if memory_context:
            augmented_transcript += f"\n\nRelevant memory:\n{memory_context}"

        # 2. Analyze with LLM
        result = analyze_feelings(
            augmented_transcript,
            user,
            datetime.now().isoformat(),
            image=screenshot,
            past_context=past_context
        )

        print("\n CHAIN OF THOUGHT:\n", result["cot"], "\n")

        # 3. Store only if user asked
        import uuid

        if should_store:
            fact_id = str(uuid.uuid4())
            confirmation_id = str(uuid.uuid4())
            
            print(f"Storing fact: {transcript} (id={fact_id})")
            self.memory.add(
                transcript,
                metadata={"type": "fact"},
                id=fact_id
            )

            print(f" Storing confirmation: {result['final']} (id={confirmation_id})")
            self.memory.add(
                result["final"],
                metadata={"type": "confirmation"},
                id=confirmation_id
            )

            # Debug: print everything after add
            print("Current memory state:")
            self.memory.print_all()

            return f"Okay {user}, I have memorized that."


        return result["final"]


