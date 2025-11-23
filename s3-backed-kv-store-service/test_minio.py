#!/usr/bin/env python3
"""Test script for MinIO service connectivity and operations."""

import os
import sys
from src.io.minio import MinioClient
from src.config import minio_settings


def test_minio_connection():
    """Test basic connectivity to MinIO service."""
    print("Testing MinIO connection...")
    try:
        client = MinioClient()
        print(f"✓ Successfully connected to MinIO at {minio_settings.ENDPOINT}")
        print(f"✓ Using bucket: {minio_settings.BUCKET}")
        return client
    except Exception as e:
        print(f"✗ Failed to connect to MinIO: {e}")
        return None


def test_put_get_operations(client: MinioClient):
    """Test put and get operations."""
    print("\nTesting put/get operations...")
    
    test_key = "test-key-123"
    test_value = b"Hello, MinIO! This is a test value."
    
    try:
        # Test put
        print(f"  Putting key '{test_key}'...")
        client.put_object(test_key, test_value)
        print(f"  ✓ Successfully put object")
        
        # Test get
        print(f"  Getting key '{test_key}'...")
        retrieved_value = client.get_object(test_key)
        print(f"  ✓ Successfully retrieved object")
        
        # Verify data integrity
        if retrieved_value == test_value:
            print(f"  ✓ Data integrity verified: values match")
        else:
            print(f"  ✗ Data mismatch! Expected {len(test_value)} bytes, got {len(retrieved_value)} bytes")
            return False
            
        return True
    except Exception as e:
        print(f"  ✗ Operation failed: {e}")
        return False


def test_multiple_operations(client: MinioClient):
    """Test multiple put/get operations."""
    print("\nTesting multiple operations...")
    
    test_cases = [
        ("key1", b"value1"),
        ("key2", b"value2"),
        ("nested/path/key", b"nested value"),
        ("key-with-special-chars-!@#", b"special value"),
    ]
    
    try:
        # Put all objects
        for key, value in test_cases:
            client.put_object(key, value)
        print(f"  ✓ Successfully put {len(test_cases)} objects")
        
        # Get all objects and verify
        for key, expected_value in test_cases:
            retrieved_value = client.get_object(key)
            if retrieved_value != expected_value:
                print(f"  ✗ Mismatch for key '{key}'")
                return False
        print(f"  ✓ Successfully retrieved and verified {len(test_cases)} objects")
        
        return True
    except Exception as e:
        print(f"  ✗ Multiple operations test failed: {e}")
        return False


def main():
    """Run all MinIO tests."""
    print("=" * 60)
    print("MinIO Service Test")
    print("=" * 60)
    print(f"Endpoint: {minio_settings.ENDPOINT}")
    print(f"Bucket: {minio_settings.BUCKET}")
    print(f"Access Key: {minio_settings.ACCESS_KEY}")
    print("=" * 60)
    
    # Test connection
    client = test_minio_connection()
    if not client:
        print("\n✗ Connection test failed. Make sure MinIO is running.")
        print("  Start MinIO with: just minio")
        sys.exit(1)
    
    # Test basic operations
    if not test_put_get_operations(client):
        print("\n✗ Basic operations test failed.")
        sys.exit(1)
    
    # Test multiple operations
    if not test_multiple_operations(client):
        print("\n✗ Multiple operations test failed.")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✓ All tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    main()

