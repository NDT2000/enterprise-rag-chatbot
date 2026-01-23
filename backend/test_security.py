from app.core.security import hash_password, verify_password, create_access_token, decode_access_token

def test_password_hashing():
    """Test password hashing and verification."""
    print("🔐 Testing Password Hashing...")
    
    password = "mysecretpassword123"
    
    # Hash the password
    hashed = hash_password(password)
    print(f"✓ Original: {password}")
    print(f"✓ Hashed: {hashed[:50]}...")
    
    # Verify correct password
    assert verify_password(password, hashed), "Password verification failed!"
    print("✓ Correct password verified!")
    
    # Verify wrong password
    assert not verify_password("wrongpassword", hashed), "Wrong password should not verify!"
    print("✓ Wrong password rejected!")
    
    print()


def test_jwt_tokens():
    """Test JWT token creation and validation."""
    print("🎫 Testing JWT Tokens...")
    
    # Create token
    user_email = "test@example.com"
    token = create_access_token({"sub": user_email})
    print(f"✓ Created token: {token[:50]}...")
    
    # Decode token
    decoded_email = decode_access_token(token)
    assert decoded_email == user_email, "Token decoding failed!"
    print(f"✓ Decoded email: {decoded_email}")
    
    # Test invalid token
    invalid_email = decode_access_token("invalid.token.here")
    assert invalid_email is None, "Invalid token should return None!"
    print("✓ Invalid token rejected!")
    
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("Security Functions Test")
    print("=" * 60)
    print()
    
    test_password_hashing()
    test_jwt_tokens()
    
    print("=" * 60)
    print("✅ All security tests passed!")
    print("=" * 60)