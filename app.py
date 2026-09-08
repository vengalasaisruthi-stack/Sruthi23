import streamlit as st
import requests

API_URL = "https://sruthi-t1fm.onrender.com"

st.set_page_config(
    page_title="Task Management System",
    page_icon="✅",
    layout="centered"
)

st.title("✅ Task Management System")

# Create Task
st.header("Create New Task")

title = st.text_input("Task Title")
description = st.text_area("Task Description")

if st.button("Add Task"):
    if title.strip():
        response = requests.post(
            f"{API_URL}/tasks",
            json={
                "title": title,
                "description": description,
                "completed": False
            }
        )

        if response.status_code == 200:
            st.success("Task added successfully!")
            st.rerun()
        else:
            st.error("Failed to add task.")
    else:
        st.warning("Please enter a task title.")


# Display Tasks
st.header("My Tasks")

try:
    response = requests.get(f"{API_URL}/tasks")

    if response.status_code == 200:
        tasks = response.json()

        if not tasks:
            st.info("No tasks available.")

        for task in tasks:
            st.subheader(task["title"])

            if task["description"]:
                st.write(task["description"])

            if task["completed"]:
                st.success("Completed")
            else:
                st.warning("Pending")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Complete", key=f"complete_{task['id']}"):
                    requests.put(
                        f"{API_URL}/tasks/{task['id']}",
                        json={
                            "title": task["title"],
                            "description": task["description"],
                            "completed": True
                        }
                    )
                    st.rerun()

            with col2:
                if st.button("Delete", key=f"delete_{task['id']}"):
                    requests.delete(
                        f"{API_URL}/tasks/{task['id']}"
                    )
                    st.rerun()

            st.divider()

except requests.exceptions.ConnectionError:
    st.error("Backend is not running. Start FastAPI first.")