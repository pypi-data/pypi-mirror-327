## Byterat Library Documentation

**Welcome to the Byterat library documentation!**

This Python library provides tools for interacting with the Byterat API, allowing you to access and analyze your battery data.

### Key Features

- Data Retrieval: Easily fetch battery observation metrics, dataset cycle data, and metadata.
- Filtering: Refine your data retrieval using flexible filter options.
- Asynchronous Operations: Perform efficient data retrieval using asynchronous functions.
- Data Handling: Work with data in a structured format using pandas DataFrames.

### Installation

```bash
pip install byterat
```

### Usage

**1. Initialization:**

```python
from byterat.sync.client import Client as ByteratClientSync
from byterat.async_.client import Client as ByteratClientAsync

# For synchronous operations
sync_client = ByteratClientSync(token="YOUR_API_TOKEN")

# For asynchronous operations
async_client = ByteratClientAsync(token="YOUR_API_TOKEN")
```

**2. Data Retrieval:**

- **Get Battery Observation Metrics:**

```python
# Get all battery observation metrics
observation_data = sync_client.get_observation_metrics()

# Get observation metrics by dataset key
observation_data_by_key = sync_client.get_observation_metrics_by_dataset_key(dataset_key="your_battery_dataset_key")

# Get observation metrics by dataset key and cycle
observation_data_by_key_cycle = sync_client.get_observation_metrics_by_dataset_key_and_dataset_cycle(
    dataset_key="your_battery_dataset_key", dataset_cycle=1
)

# Get observation metrics by filename
observation_data_by_filename = sync_client.get_observation_metrics_by_filename(file_name="your_battery_data.csv")
```

- **Get Battery Dataset Cycle Data:**

```python
# Get all battery dataset cycle data
cycle_data = sync_client.get_dataset_cycle_data()

# Get dataset cycle data by dataset key
cycle_data_by_key = sync_client.get_dataset_cycle_data_by_dataset_key(dataset_key="your_battery_dataset_key")

# Get dataset cycle data by dataset key and cycle
cycle_data_by_key_cycle = sync_client.get_dataset_cycle_data_by_dataset_key_and_dataset_cycle(
    dataset_key="your_battery_dataset_key", dataset_cycle=1
)

# Get dataset cycle data by filename
cycle_data_by_filename = sync_client.get_dataset_cycle_data_by_filename(file_name="your_battery_data.csv")
```

- **Get Battery Metadata:**

```python
# Get all battery metadata
metadata = sync_client.get_metadata()

# Get metadata by dataset key
metadata_by_key = sync_client.get_metadata_by_dataset_key(dataset_key="your_battery_dataset_key")
```

**3. Filtering:**

```python
from byterat.filter import Filter, FilterOperator, FilterGroup, FilterGroupType

# Create filters
filter1 = Filter(column="voltage", operator=FilterOperator.GT, value=3.5)
filter2 = Filter(column="temperature", operator=FilterOperator.LT, value=30)

# Create a filter group
filter_group = FilterGroup([filter1, filter2], mode=FilterGroupType.AND)

# Retrieve a chunk of filtered observation data -> Returns a ByteratData object
filtered_observation_data = sync_client.get_filtered_observation_data(filters=filter_group)

# Retrieve all filtered observation data (all chunks) -> Returns a DataFrame containing all data matching filters
all_filtered_observation_data = sync_client.get_all_filtered_observation_data(filters=filter_group)

# Retrieve a chunk of filtered dataset cycle data -> Returns a ByteratData object
filtered_cycle_data = sync_client.get_filtered_dataset_cycle_data(filters=filter_group)

# Retrieve all filtered dataset cycle data (all chunks) -> Returns a DataFrame containing all data matching filters
all_filtered_cycle_data = sync_client.get_all_filtered_dataset_cycle_data(filters=filter_group)

# Retrieve a chunk of filtered metadata -> Returns a ByteratData object
filtered_metadata = sync_client.get_filtered_metadata(filters=filter_group)

# Retrieve all filtered metadata (all chunks) -> Returns a DataFrame containing all data matching filters
all_filtered_metadata = sync_client.get_all_filtered_metadata(filters=filter_group)
```

**4. Asynchronous Operations:**

```python
import asyncio

async def main():
    # Use async_client for asynchronous operations
    observation_data = await async_client.get_observation_metrics()
    #... (other asynchronous methods)

asyncio.run(main())
```

**5. Data Handling:**

The retrieved data is returned as a `ByteratData` object, which contains a `pandas` DataFrame (`data`) and a continuation token (`continuation_token`) for handling paginated results.

```python
# Access the DataFrame
df = observation_data.data

# Use pandas functionalities for data analysis and manipulation
print(df.head())
#...
```

**6. Handling Paginated Results**

The Byterat API uses a continuation token for pagination. When you request data, and the result set is large, the API will only return a portion of the data along with a continuation token. This token acts as a pointer to the next chunk of data.

After making a request to the Byterat API (e.g., `get_observation_metrics`), the response will include:

- `data`: A `pandas` DataFrame containing the current chunk of data.
- `continuation_token`: A string that can be used to fetch the next chunk of data. If this is `None`, then there is no more data to retrieve.

To get the next chunk of data, simply pass this `continuation_token` back to the same API function as an argument.

```python
from byterat.sync.client import Client as ByteratClientSync

# Initialize the client
client = ByteratClientSync(token="YOUR_API_TOKEN")

# Fetch the first batch of data
response = client.get_observation_metrics()

# Process the first batch
if not response.data.empty:
    print(response.data.head())

    # Keep fetching and processing data until no more is available
    while response.continuation_token is not None:  # Correct termination condition
        # Fetch the next batch using the token
        response = client.get_observation_metrics(continuation_token=response.continuation_token)

        # Process the next batch
        if not response.data.empty:
            print(response.data.head())
```

**Important Considerations**

- Efficiency: Retrieving data in chunks can be more efficient than trying to download a massive dataset all at once.
- Large Datasets: For very large datasets, consider using asynchronous operations to avoid blocking your application while waiting for data.
- State: The continuation token represents a specific point in the data. If the underlying data changes significantly, the token may become invalid.

### Class and Function Explanations

- `Client` (sync and async): This class provides the main interface for interacting with the Byterat API. It handles authentication, data retrieval, and filtering.
- `get_observation_metrics`: Retrieves battery observation metrics data. You can filter by dataset key, dataset cycle, or filename.
- `get_dataset_cycle_data`: Retrieves battery dataset cycle data. You can filter by dataset key, dataset cycle, or filename.
- `get_metadata`: Retrieves battery metadata. You can filter by dataset key.
- `get_filtered_observation_data`: Retrieves a single chunk of observation data filtered by the provided filter group.
- `get_all_filtered_observation_data`: Retrieves all observation data that matches the filter by retrieving data in chunks until no continuation token is returned.
- `get_filtered_dataset_cycle_data`: Retrieves a single chunk of dataset cycle data filtered by the provided filter group.
- `get_all_filtered_dataset_cycle_data`: Retrieves all dataset cycle data that matches the filter by retrieving data in chunks until no continuation token is returned.
- `get_filtered_metadata`: Retrieves a single chunk of metadata filtered by the provided filter group.
- `get_all_filtered_metadata`: Retrieves all metadata that matches the filter by retrieving data in chunks until no continuation token is returned.
- `Filter`: Represents a single filter condition.
- `FilterOperator`: Defines the available filter operators (e.g., equals, greater than, contains).
- `FilterGroup`: Combines multiple filters using logical operators (AND, OR). FilterGroups can be nested within each other to create complex filter conditions.
- `ByteratData`: A container class that holds the retrieved data as a pandas DataFrame and a continuation token for pagination.

### Building Complex Filters with FilterGroup

The `FilterGroup` class allows you to create complex filter expressions by combining multiple `Filter` objects or even other `FilterGroup` objects. This recursive structure enables you to build sophisticated filtering logic.

**Example:**

```python
from byterat.filter import Filter, FilterOperator, FilterGroup, FilterGroupType

# Create individual filters
filter1 = Filter(column="cycle_count", operator=FilterOperator.GT, value=100)
filter2 = Filter(column="state_of_charge", operator=FilterOperator.EQ, value=1.0)
filter3 = Filter(column="manufacturer", operator=FilterOperator.EQ, value="Tesla")

# Create a nested FilterGroup
battery_filter = FilterGroup([filter2, filter3], mode=FilterGroupType.AND)

# Combine with the cycle count filter
combined_filter = FilterGroup([filter1, battery_filter], mode=FilterGroupType.AND)

# Use the combined filter to retrieve data
filtered_data = sync_client.get_all_filtered_observation_data(filters=combined_filter)
```

In this example, `battery_filter` combines the state of charge and manufacturer filters with an AND condition. Then, `combined_filter` further combines the `battery_filter` with the cycle count filter, again using an AND condition. This results in a filter that selects data where the cycle count is greater than 100 AND the state of charge is 1.0 AND the manufacturer is Tesla.

By nesting and chaining `FilterGroup` objects, you can express arbitrarily complex filter conditions to precisely target the data you need.

### Additional Notes

- Error Handling: The library may raise exceptions for invalid input or API errors. Make sure to handle exceptions appropriately in your code.
- Asynchronous vs. Synchronous: Choose the appropriate client (ByteratClientSync or ByteratClientAsync) based on your application's needs.
- Filtering: The library offers a variety of filter operators for precise data selection.
- Pagination: Use the continuation token to retrieve subsequent pages of data when dealing with large datasets.
