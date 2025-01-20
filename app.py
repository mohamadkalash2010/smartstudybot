import streamlit as st
from groq import Groq

def generate_study_plan(duration, topics):
    plan = []
    days = max(1, duration)  # Ensure at least 1 day for preparation
    topics_per_day = max(1, len(topics) // days)

    for day in range(1, days + 1):
        start = (day - 1) * topics_per_day
        end = start + topics_per_day
        day_topics = topics[start:end]
        plan.append(f"Day {day}: Study {', '.join(day_topics)}")

    return plan

def get_resources(topic):
    client = Groq()
    stream = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "you are a helpful assistant."},
            {"role": "user", "content": f"Provide resources like videos, worksheets, and quizzes for {topic}."}
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        max_completion_tokens=1024,
        top_p=1,
        stop=None,
        stream=True,
    )

    resources = ""
    for chunk in stream:
        resources += chunk.choices[0].delta.content

    return resources

def main():
    st.title("Student Study Bot")

    # Introduction
    st.write("Hi! I'm here to help you prepare for your exams.")

    # Step 1: Ask for the purpose
    purpose = st.text_input("What is the topic or subject of your exam?")

    if purpose:
        st.write(f"Great! Let's prepare for your {purpose} exam.")

        # Step 2: Ask for duration
        duration = st.number_input("How many days do you have until the exam?", min_value=1, step=1)

        if duration:
            st.write(f"You have {duration} day(s) to prepare.")

            # Step 3: Ask for topics
            topics = st.text_area("List the lessons or topics you need to cover (separate by commas):")

            if topics:
                topic_list = [t.strip() for t in topics.split(',')]
                
                # Generate study plan
                study_plan = generate_study_plan(duration, topic_list)

                st.subheader("Your Study Plan:")
                for day_plan in study_plan:
                    st.write(day_plan)

                # Provide resources
                st.subheader("Resources for Your Topics:")
                for topic in topic_list:
                    st.write(f"### {topic}")
                    resources = get_resources(topic)
                    st.write(resources)

if __name__ == "__main__":
    main()
