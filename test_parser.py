from log_parser import parse_log_file

# Read application logs
result = parse_log_file("logs/application.log")

# Extract parsed entries
df = result["entries"]

print("\nAPPLICATION LOGS")
print(df.to_string(index=False))

print("\nLOG SUMMARY")
print(result["counts"].to_string(index=False))

print("\nERROR MESSAGES")
print(result["error_messages"].to_string(index=False))

print("\nINVALID LINES")
print(result["invalid_lines"].to_string(index=False))