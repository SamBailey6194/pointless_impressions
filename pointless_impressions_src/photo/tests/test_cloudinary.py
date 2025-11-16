"""
Test Cloudinary connection directly without Django
Run this from your project root: python test_cloudinary.py
"""

import cloudinary
from cloudinary import api

# Configure directly with your credentials
cloudinary.config(
    cloud_name='djdhyhznc',
    api_key='598698126349722',
    api_secret='cO3sQCq-TGpY81NVnDMLY8w8xuQ',
    secure=True
)

print("=" * 60)
print("Testing Cloudinary Connection")
print("=" * 60)
print(f"Cloud name: {cloudinary.config().cloud_name}")
print(f"API key: {cloudinary.config().api_key}")
print(f"Secure: {cloudinary.config().secure}")
print("=" * 60)

try:
    print("\nTesting API connection...")
    
    # Try to get all resources (no filter)
    response = api.resources(
        type='upload',
        max_results=10
    )
    
    resources = response.get('resources', [])
    print(f"\n✓ Success! Found {len(resources)} resources")
    
    if resources:
        print("\nFirst few public_ids:")
        for i, resource in enumerate(resources[:5], 1):
            print(f"  {i}. {resource['public_id']}")
    
    print("\n" + "=" * 60)
    print("Connection test PASSED!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n✗ Error: {type(e).__name__}")
    print(f"  Details: {e}")
    print("\n" + "=" * 60)
    print("Connection test FAILED!")
    print("=" * 60)
