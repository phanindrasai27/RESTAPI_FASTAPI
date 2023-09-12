import streamlit as st
import requests

# Define the base URL of your FastAPI API
BASE_URL = "http://127.0.0.1:8000"  # Replace with your API URL

# Function to fetch all servers from the API
def fetch_servers():
    response = requests.get(f"{BASE_URL}/servers")
    return response.json()

# Function to create a new server
def create_server(server_data):
    response = requests.post(f"{BASE_URL}/servers/", json=server_data)
    return response.json()

# Function to delete a server by ID
def delete_server(server_id):
    response = requests.delete(f"{BASE_URL}/servers/{server_id}")
    return response.status_code

# Streamlit app
def main():
    st.title("Server Management UI")

    # Display a list of servers
    servers = fetch_servers()
    st.subheader("Server List")
    for server in servers:
        st.write(f"Server ID: {server['id']}, Name: {server['name']}")

    # Create a new server
    st.subheader("Create New Server")
    new_server_name = st.text_input("Enter Server Name:")
    if st.button("Create"):
        if new_server_name:
            new_server_data = {"name": new_server_name}
            created_server = create_server(new_server_data)
            st.success(f"Server created with ID: {created_server['id']}")
        else:
            st.error("Please enter a server name.")

    # Delete a server
    st.subheader("Delete Server")
    delete_server_id = st.text_input("Enter Server ID to delete:")
    if st.button("Delete"):
        if delete_server_id:
            status_code = delete_server(delete_server_id)
            if status_code == 200:
                st.success(f"Server with ID {delete_server_id} deleted.")
            else:
                st.error(f"Failed to delete server with ID {delete_server_id}.")
        else:
            st.error("Please enter a server ID to delete.")

if __name__ == "__main__":
    main()
