# trough-id
identify the main ionospheric trough in total electron content images

desired usage: `python -m trough-id --start-date MMDDYYYY --end-date MMDDYYYY --output-dir /path/to/dir`

* downloads madrigal
* downloads Kp
* downloads auroral boundary
* runs TEC preparation
* runs trough identification
* saves in logical directory structure
* nice functions for accessing all underlying data, most importantly prepared TEC and trough ids

for fine-grained control: `python -m trough-id --config /path/to/config`