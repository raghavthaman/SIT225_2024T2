import streamlit as st
import pandas as pd
import plotly.express as px
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from datetime import datetime

# Set page config
st.set_page_config(page_title="Gyroscope Dashboard", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .stDataFrame {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# File watcher for continuous data updates
class CSVHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback
    
    def on_modified(self, event):
        if event.src_path.endswith('.csv'):
            self.callback()

# Load data function with caching
@st.cache_data(ttl=10)  # Refresh cache every 10 seconds
def load_data(file_path='gyroscope_data.csv'):
    try:
        data = pd.read_csv(file_path)
        # Convert timestamp to datetime if it exists
        if 'timestamp' in data.columns:
            try:
                data['timestamp'] = pd.to_datetime(data['timestamp'])
            except:
                # If conversion fails, create a simple timestamp
                data['timestamp'] = pd.to_datetime(data.index, unit='s')
        return data
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame(columns=['timestamp', 'x', 'y', 'z'])

# Initialize session state for pagination
if 'page_num' not in st.session_state:
    st.session_state.page_num = 0

# Main dashboard function
def main():
    st.title("Gyroscope Data Dashboard")
    st.write("Interactive visualization of gyroscope data from Arduino Nano 33 IoT")
    
    # Load data
    data = load_data()
    
    if data.empty:
        st.warning("No data found. Please ensure the CSV file exists and contains data.")
        return
    
    # Dashboard controls in sidebar
    with st.sidebar:
        st.header("Controls")
        
        # Graph type selection
        graph_type = st.selectbox(
            "Select Graph Type",
            ["Line Chart", "Scatter Plot", "Histogram", "Box Plot", "Violin Plot"]
        )
        
        # Variable selection
        selected_vars = st.multiselect(
            "Select Variables",
            ['x', 'y', 'z'],
            default=['x', 'y', 'z']
        )
        
        # Sample size control
        total_samples = len(data)
        samples_per_page = st.number_input(
            "Samples per page",
            min_value=10,
            max_value=total_samples,
            value=min(100, total_samples),
            step=10
        )
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Previous") and st.session_state.page_num > 0:
                st.session_state.page_num -= 1
        with col2:
            max_pages = total_samples // samples_per_page
            if st.button("Next") and st.session_state.page_num < max_pages:
                st.session_state.page_num += 1
        
        st.write(f"Showing page {st.session_state.page_num + 1} of {max_pages + 1}")
        
        # Auto-refresh toggle
        auto_refresh = st.checkbox("Auto-refresh (10s)", value=True)
        
        # Data info
        st.header("Data Info")
        st.write(f"Total samples: {total_samples}")
        if 'timestamp' in data.columns:
            st.write(f"Last updated: {data['timestamp'].max()}")

    # Calculate data range to display
    start_idx = st.session_state.page_num * samples_per_page
    end_idx = start_idx + samples_per_page
    display_data = data.iloc[start_idx:end_idx]
    
    # Main visualization area
    st.header("Data Visualization")
    
    try:
        # Create appropriate visualization based on selection
        if graph_type == "Line Chart":
            fig = px.line(
                display_data,
                x='timestamp' if 'timestamp' in display_data.columns else display_data.index,
                y=selected_vars,
                title=f"Gyroscope Data - {graph_type}",
                labels={'value': 'Angular Velocity (rad/s)'}
            )
        elif graph_type == "Scatter Plot":
            if len(selected_vars) >= 2:
                fig = px.scatter(
                    display_data,
                    x=selected_vars[0],
                    y=selected_vars[1],
                    title=f"Gyroscope Data - {graph_type}",
                    labels={'value': 'Angular Velocity (rad/s)'}
                )
            else:
                st.warning("Select at least 2 variables for scatter plot")
                return
        elif graph_type == "Histogram":
            fig = px.histogram(
                display_data,
                x=selected_vars,
                title=f"Gyroscope Data - {graph_type}",
                labels={'value': 'Angular Velocity (rad/s)'},
                marginal="rug",
                barmode="overlay"
            )
        elif graph_type == "Box Plot":
            fig = px.box(
                display_data,
                y=selected_vars,
                title=f"Gyroscope Data - {graph_type}",
                labels={'value': 'Angular Velocity (rad/s)'}
            )
        elif graph_type == "Violin Plot":
            fig = px.violin(
                display_data,
                y=selected_vars,
                title=f"Gyroscope Data - {graph_type}",
                labels={'value': 'Angular Velocity (rad/s)'},
                box=True
            )
        
        # Display the plot
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating visualization: {str(e)}")
    
    # Data summary table
    st.header("Data Summary")
    summary_data = display_data[selected_vars].describe()
    st.dataframe(summary_data)
    
    # Raw data display
    with st.expander("View Raw Data"):
        st.dataframe(display_data[selected_vars])
    
    # Auto-refresh logic
    if auto_refresh:
        time.sleep(10)
        st.rerun()

# Set up file watcher if needed
if not hasattr(st.session_state, 'watcher_setup'):
    try:
        path = os.path.dirname(os.path.abspath('gyroscope_data.csv'))
        event_handler = CSVHandler(lambda: st.rerun())
        observer = Observer()
        observer.schedule(event_handler, path, recursive=False)
        observer.start()
        st.session_state.watcher_setup = True
    except Exception as e:
        st.error(f"Could not set up file watcher: {str(e)}")

if __name__ == "__main__":
    main()