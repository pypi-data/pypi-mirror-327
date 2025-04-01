from viindex import create_indexer


def main():
    # Create or connect to the database
    indexer = create_indexer("my_videos.db")

    # Index a new video
    video_id = indexer.index_video(
        "/path/to/video.mp4",
        {"title": "My Sample Video", "duration": 120, "tags": ["sample", "demo"]},
    )
    print(f"Indexed video with ID: {video_id}")

    # Retrieve the video by ID
    video_record = indexer.get_video_by_id(video_id)
    print("Retrieved video record:", video_record)

    # Update the metadata
    success = indexer.update_video_metadata(video_id, {"title": "Updated Title"})
    if success:
        print(f"Successfully updated metadata for video ID: {video_id}")

    # Search for videos with the keyword "sample"
    results = indexer.search_videos("sample")
    print("Search results for 'sample':", results)

    # Remove the video
    indexer.remove_video(video_id)
    print(f"Removed video with ID: {video_id}")

    # Close the database connection
    indexer.close()


if __name__ == "__main__":
    main()
