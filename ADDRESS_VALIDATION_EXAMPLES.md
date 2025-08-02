# Address Validation Examples

## ✅ VALID Addresses (These will be accepted):
- "Victoria Island, Lagos, Nigeria"
- "Ikeja GRA, Lagos State"
- "Plot 123, Ademola Adetokunbo Street, Wuse 2, Abuja"
- "University of Lagos, Akoka"
- "Lekki Phase 1, Lagos"
- "Ring Road, Ibadan, Oyo State"

## ❌ INVALID Inputs (These will be rejected):
- "6.4281, 3.4219" ← Coordinates
- "-6.5, 3.4" ← Negative coordinates  
- "6.123456, 3.654321" ← Decimal coordinates
- "123" ← Too short
- "" ← Empty

## Error Messages:
When coordinates are entered, users will see:
- **For pickup**: "Please enter a street address (e.g., 'Victoria Island, Lagos') instead of coordinates"
- **For dropoff**: "Please enter a street address (e.g., 'Ikeja, Lagos') instead of coordinates"

## Why This Matters:
1. **Driver Experience**: Drivers see meaningful locations instead of numbers
2. **User Experience**: Prevents accidental coordinate entry
3. **Data Quality**: Ensures readable, searchable address data
4. **Communication**: Drivers can easily find and communicate about locations

## Testing the Validation:

The error you saw: `"Please enter a street address, not coordinates"` is **EXPECTED BEHAVIOR**.

This means the validation is working correctly and preventing coordinate input, which is exactly what we want!

### In the test:
- ✅ "Victoria Island, Lagos, Nigeria" → **Accepted** (valid address)
- ❌ "6.4281, 3.4219" → **Rejected** (coordinates) ← This is the error you saw

This validation error is a **feature, not a bug**!
