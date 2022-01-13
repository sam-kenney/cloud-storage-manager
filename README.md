# Google Cloud Storage Manager
This library is used to operate over the Google Cloud Storage SDKs.


## Credentials
Make a copy of the `env_template` file and call it .env. You only need to provide one variable to export here, that being `GOOGLE_APPLICATION_CREDENTIALS`. This needs to be the path to your [credentials file](https://cloud.google.com/iam/docs/creating-managing-service-account-keys#iam-service-account-keys-create-console).


## Creating an environment
Create a virtual development environment by using the `virtualenv` Python library. You can install this by executing `pip3 install virtualenv`. 

To create your environment, type `virtualenv {your-env}`. Once created, you must activate it by using `source {your-env}/bin/activate`. Once you are done developing, simply type `deactivate` in your terminal.


## Installation

### Implementing the library
*   Install the library by running `pip install git+ssh://github.com/mr-strawberry66/cloud-storage-manager`. This will use your existing ssh credentials in order to install the library. 
*   You can also place `git+ssh://github.com/mr-strawberry66/cloud-storage-manager` in a requirements.txt file for a project. 

### Developing for the library
*   Install the required Python libraries using `pip install -r requirements.txt`.
*   If you are developing for this tool, install the Python libraries required by running `pip install -r dev-requirements.txt`.

*Please ensure to create your environment before you execute any of the installation commands*

## Using the CloudStorage Class
The `CloudStorage` Class has a couple of parameters, both of which are optional. 

| Parameter | Use |
|---|---|
| gcp_project_id | The ID of the GCP Project you are working within. While passing it in as a parameter is optional, the GCP Project ID must be provided somehow. You may either do this via the parameter when instantiating the Class, or you may pass it in as an environment variable, as `GCP_PROJECT_ID`. |
| default_bucket | This is an entirely optional parameter. Use only if you are reading and writing to the same bucket in multiple operations. This parameter is overwritten by the `bucket` parameter in all of the Class methods. |

### Downloading a file
```py
import os
from cloud_storage_manager import CloudStorage

cs = CloudStorage()

file = cs.download_file(
  bucket="test-cs-download",
  gcs_file_name="name_of_file.txt",
  destination_file_path=os.path.join(".", "destination"),
)
```

### Uploading a file
```py
import os
from cloud_storage_manager import CloudStorage

cs = CloudStorage()

resp = cs.upload_file(
  bucket="test-cs-upload",
  file_name=os.path.join(".", "destination", "name_of_file.txt"),
  tmp_file=False,
)
```

### Reading a file's contents directly from Cloud Storage
In some cases you may not care about storing a file locally, for example, if you wanted to access a refresh token hosted in Google Cloud Storage. In this case, you can use the `read_text()` method to extract the contents of a file, and store it in a variable.
```py
from cloud_storage_manager import CloudStorage

cs = CloudStorage()

"""
Note there are methods for different file types,
including json and ndjson, both of which will load
the data as a list of dicts for easy manipulation.
Methods are cs.read_json() and cs.read_ndjson().
"""

data = cs.read_text(
  bucket="test-cs-upload",
  gcs_file_name="name_of_file.txt",
)
```

### Uploading data directly to Cloud Storage
The `ndjson` file format can be onboarded directly to a BigQuery table. The `upload_ndjson()` method takes a lot of the work out of formatting a list of dicts and creates an easy to onboard file in Cloud Storage.

There are methods to upload regular `json`, and `str` data also. These are `upload_json()` and `upload_text()`.
```py
from cloud_storage_manager import CloudStorage

cs = CloudStorage()

data = [
  {
    "Name": "Peter",
    "Role": "Analytics Engineer",
  },
  {
    "Name": "Jane",
    "Role": "Programmatic Specialist",
  }
]

file = cs.upload_ndjson(
  data=data,
  file_name="employees.ndjson",
  bucket="test-cs-upload",
)
```
Output file:
```json
  {"Name": "Peter", "Role": "Analytics Engineer"}
  {"Name": "Jane", "Role": "Programmatic Specialist"}
```
