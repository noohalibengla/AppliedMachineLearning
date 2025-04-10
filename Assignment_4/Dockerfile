FROM python:3.10-slim

# Set working directorydocker run -d -p 5000:5000 --name score-container flask-score-app in the container
WORKDIR /app

# Copy necessary files
COPY auxilary.py app.py score.py svm.pkl custom_vectorizer.pkl requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your Flask app runs on
EXPOSE 5000

# Start the Flask app
CMD ["python", "app.py"]