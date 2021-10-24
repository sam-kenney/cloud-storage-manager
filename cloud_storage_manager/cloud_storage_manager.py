"""Functions to utilise the Google Cloud Storage client library."""
import json
import os
from typing import List
from google.cloud import storage


class CloudStorage:
    """Operate on Google Cloud Storage client library."""

    def __init__(
        self,
        gcp_project_id: str = None,
        default_bucket: str = None,
    ) -> None:
        """
        Initialise the Class.

        args:
            gcp_project_id: str
                The GCP project ID
                to access cloud storage.
                Will attempt to retrieve
                this from the environment.

            default_bucket: str
                Use if you are reading and
                writing to the same place.
                Is overwritten by the bucket
                parameter in each other
                function.
        """
        self.gcp_project_id = os.environ.get(
            "GCP_PROJECT_ID",
            gcp_project_id,
        )
        self.client = storage.Client(self.gcp_project_id)
        self.default_bucket = default_bucket

    def _set_bucket(self, bucket: str) -> str:
        """
        Set the bucket to read from / write to.

        bucket: str
            A bucket provided in a read/write
            function.

        return: str
            The correct bucket to use.

        except: ValueError
            If no bucket is provided.
        """
        _bucket = bucket or self.default_bucket
        if not _bucket:
            raise ValueError("No bucket provided")
        return _bucket

    def download_file(
        self,
        bucket: str = None,
        gcs_file_name: str = None,
        destination_file_path: str = None,
    ) -> str:
        """
        Download a file from Google Cloud Storage.

        args:
            bucket: str
                The bucket to collect the
                file from.

            gcs_file_name: str
                The file to retrieve from
                the specified bucket.

            destination_file_path: str
                Where to write the file
                to.

        return: str
            A success message.
        """
        if not gcs_file_name:
            raise ValueError("No file provided")
        gcs_bucket = self.client.get_bucket(
            self._set_bucket(bucket=bucket),
        )
        blob = gcs_bucket.get_blob(gcs_file_name)
        blob.download_to_filename(destination_file_path)
        return destination_file_path

    def read_text(
        self,
        bucket: str = None,
        gcs_file_name: str = None,
        encoding: str = "utf-8",
    ) -> str:
        """
        Read the contents of a file from Cloud Storage.

        args:
            bucket: str
                The bucket to collect the
                file from.

            gcs_file_name: str
                The file to retrieve from
                the specified bucket.

            encoding: str
                The character encoding used
                in the file. Defaults to
                utf-8.

        return: str
            The contents of the file.
        """
        if not gcs_file_name:
            raise ValueError("No file provided")
        gcs_bucket = self.client.get_bucket(
            self._set_bucket(bucket=bucket),
        )
        blob = gcs_bucket.get_blob(gcs_file_name)
        data = blob.download_as_string().decode(encoding)
        return data

    def read_json(
        self,
        bucket: str = None,
        gcs_file_name: str = None,
        encoding: str = "utf-8",
    ) -> List[dict]:
        """
        Read the contents of a json file from Cloud Storage.

        args:
            bucket: str
                The bucket to collect the
                file from.

            gcs_file_name: str
                The file to retrieve from
                the specified bucket.

            encoding: str
                The character encoding used
                in the file. Defaults to
                utf-8.

        return: List[dict]
            The loaded contents of the file.
        """
        data = self.read_text(
            bucket=bucket,
            gcs_file_name=gcs_file_name,
            encoding=encoding,
        )
        return json.loads(data)

    def read_ndjson(
        self,
        bucket: str = None,
        gcs_file_name: str = None,
        encoding: str = "utf-8",
    ) -> List[dict]:
        """
        Read the contents of a newline delimited json file from Cloud Storage.

        args:
            bucket: str
                The bucket to collect the
                file from.

            gcs_file_name: str
                The file to retrieve from
                the specified bucket.

            encoding: str
                The character encoding used
                in the file. Defaults to
                utf-8.

        return: List[dict]
            The loaded contents of the file.
        """
        data = self.read_text(
            bucket=bucket,
            gcs_file_name=gcs_file_name,
            encoding=encoding,
        )
        return [json.loads(row) for row in data.splitlines()]

    def upload_file(
        self,
        bucket: str = None,
        file_name: str = None,
        tmp_file: bool = True,
    ):
        """
        Upload a file to Cloud Storage.

        args:
            bucket: str
                The bucket to upload the
                file to.

            file_name: str
                The name of the file to
                upload to Cloud Storage.

            tmp_file: bool
                Whether the file is located
                in tmp storage or not. Defaults
                to True. Will run file cleanup
                if True.

        return: str
            A success message.

        except: ValueError
            If no file is provided.
        """
        if not file_name:
            raise ValueError("No file provided")
        gcs_bucket = self.client.get_bucket(
            self._set_bucket(bucket),
        )
        blob = gcs_bucket.blob(file_name)
        if tmp_file:
            file = os.path.join("/tmp", file_name)
            blob.upload_from_filename(file)
            os.remove(file)
        else:
            blob.upload_from_filename(file_name)
        return "Success"

    def upload_text(
        self,
        data: any,
        file_name: str,
        bucket: str = None,
    ):
        """
        Upload data to Cloud Storage.

        args:
            data: str
                The data to write.

            file_name: str
                The name to give the file
                in Cloud Storage.

            bucket: str
                The bucket to write the
                data to.

        return: str
            A success message.
        """
        self._create_tmp_file(
            data=data,
            file_name=file_name,
        )
        return self.upload_file(
            bucket=bucket,
            file_name=file_name,
            tmp_file=True,
        )

    def upload_json(
        self,
        data: List[dict],
        file_name: str,
        bucket: str = None,
    ):
        """
        Upload data to Cloud Storage as a json file.

        args:
            data: str
                The data to write.

            file_name: str
                The name to give the file
                in Cloud Storage.

            bucket: str
                The bucket to write the
                data to.

        return: str
            A success message.
        """
        self._create_tmp_file(
            data=json.dumps(data),
            file_name=file_name,
        )
        return self.upload_file(
            bucket=bucket,
            file_name=file_name,
            tmp_file=True,
        )

    def _create_tmp_file(
        self,
        data: any,
        file_name: str,
    ) -> str:
        """Create a json file from a list of dicts, or a dict."""
        path = os.path.join("/tmp", file_name)
        with open(path, "w") as file:
            file.write(data)
        return file_name

    def upload_ndjson(
        self,
        data: List[dict],
        file_name: str,
        bucket: str = None,
    ):
        """
        Upload data to Cloud Storage as a newline delimited json file.

        args:
            data: str
                The data to write.

            file_name: str
                The name to give the file
                in Cloud Storage.

            bucket: str
                The bucket to write the
                data to.

        return: str
            A success message.
        """
        self._create_ndjson_tmp_file(
            data=data,
            file_name=file_name,
        )
        return self.upload_file(
            bucket=bucket,
            file_name=file_name,
            tmp_file=True,
        )

    def _create_ndjson_tmp_file(
        self,
        data: List[dict],
        file_name: str,
    ) -> str:
        """Create a newline delimited json file."""
        path = os.path.join("/tmp", file_name)
        with open(path, "a") as file:
            for row in data:
                file.writelines(json.dumps(row) + "\n")
        return file_name
