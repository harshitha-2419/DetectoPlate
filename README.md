DetectoPlate 

Detect and Recognize Car License Plate from a video in real time..

The system’s workflow is as follows:
- Video Upload: The user uploads a video via the Flask web interface.
- File Validation: The system validates the file format (MP4, AVI, MOV) and stores it temporarily using os and Werkzeug.
- Frame Extraction: OpenCV extracts frames, processing up to 10 frames, skipping every 30th frame for efficiency.
- Plate Localization: The plate_detection CNN identifies plate ROIs in each processed frame.
- Text Extraction: EasyOCR extracts plate numbers from the ROIs.
- Database Query: The database_operations module queries the SQLite3 database for vehicle details using detected plate numbers.
- Result Formatting: Results are formatted as JSON, including vehicle details or “Details not found” messages.
- Display: The Flask endpoint returns the JSON response to the web interface for user viewing.
- Cleanup: Temporary video files are deleted.
can u gv me a flow diagram according to the above process flow
