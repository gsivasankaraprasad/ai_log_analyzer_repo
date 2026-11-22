
from log_parser import parse_log_file
from ai_analyzer import analyze_errors

# Read application logs
result = parse_log_file("logs/application.log")

# Extract error and critical messages
errors = result["error_messages"]

print("\nStarting AI log analysis...")
print("Sending errors to Ollama...\n")

# Get AI analysis
analysis = analyze_errors(errors)

print("=" * 60)
print("AI LOG ANALYSIS REPORT")
print("=" * 60)

print(analysis)

print("=" * 60)
