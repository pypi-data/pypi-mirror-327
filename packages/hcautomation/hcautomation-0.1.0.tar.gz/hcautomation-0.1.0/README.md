
# Inhouse Auomation Library for HC

After pip install is complete run the following in the command line. This will create a directory in your One Drive - C:\Users\266112\OneDrive - Landmark Group\Work\Automations\GUI
```python
python -m hcautomation.post_install_setup
```

To use this library, import the following class & create an object of this class using:

```python
  from hcautomation.hcautomation import Download
  obj = Download('name_of_project')
```


## Library Usage
#### QV Download
This function downloads data from a QV bookmark.
```python
obj.qv(url, save_path, download_time, column_order=[], cols_to_convert=[], typ='float', lx=False, stop_date='', extension='csv', lx_mon=[], include_today=False, check_date_filter=True)
```

Parameters starting with **!** are REQUIRED, rest are OPTIONAL
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| **!** `url` | `string` | Link to the QV bookmark |
| **!** `save_path`  | `string` |  Path with filename for the save location of file downloaded from QV |
| **!** `download_time` | `int` |  Maximum time to wait for download to finish |
| `column_order` | `list` | Order of columns to reorder columns in downloaded file |
| `cols_to_convert` | `list` | If file is downloaded as CSV, convert given list of columns to float |
| `lx` | `Boolean` | Set to True if you want to select the dates for which data has to be downloaded. |
| `stop_date` | `string` | Download data from this date onwards till today. Format: dd/mm/yyyy |
| `extension` | `string` | File format to download final data in. 'csv' or 'xlsx' |
| `lx_mon` | `string` | WIP |
| `include_today` | `Boolean` | Default False. Download today's data as well if set to True |
| `check_date_filter` | `Boolean` | Default True. Check if date filter has been applied |


#### ER Download

```python
  GET /api/items/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

#### add(num1, num2)

Takes two numbers and returns the sum.

