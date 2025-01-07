from datetime import datetime
from components.database import MediaCreate, test_bin_and_media, add_more_media_to_bin, fetch_bin_with_media

# Run the test
if __name__ == "__main__":
    test_bin_and_media()

    additional_media_items = [
        MediaCreate(date=datetime.now(), type="text", content="Another text content"),
        MediaCreate(date=datetime.now(), type="image", content="another_image.png")
    ]

    # Append the new media to the bin with bin_id = 1
    add_more_media_to_bin(bin_id=1, new_media_items=additional_media_items)

    # Fetch and display the updated bin
    fetch_bin_with_media(bin_id=1)
