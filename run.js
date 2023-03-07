const fs = require('fs');
const MongoClient = require('mongodb').MongoClient;
const axios = require('axios');

// Define the MongoDB database URL and database name
const url = 'mongodb://localhost:27017/';
const dbName = 'mydb';

// Define the OpenAI API parameters
const openaiUrl = 'https://api.openai.com/v1/completions';
const openaiApiKey = '<YOUR_OPENAI_API_KEY>';

// Read the file content
const fileContent = fs.readFileSync('file.txt', 'utf8');

// Connect to the MongoDB database
MongoClient.connect(url, { useUnifiedTopology: true }, function(err, client) {
  if (err) throw err;

  // Select the database
  const db = client.db(dbName);

  // Ask the user for a question
  const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
  });

  readline.question('Ask a question about the file: ', function(question) {
    // Save the question to the database
    const collection = db.collection('questions');
    collection.insertOne({ question: question }, function(err, result) {
      if (err) throw err;
      console.log('Question saved to database');
      client.close();

      // Send the OpenAI API request
      axios.post(openaiUrl, {
        prompt: `${fileContent}\nQuestion: ${question}\nAnswer:`,
        temperature: 0.5,
        max_tokens: 50
      }, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${openaiApiKey}`
        }
      }).then(function(response) {
        // Print the OpenAI API response and save it to the database
        console.log('OpenAI API response:', response.data.choices[0].text);
        const collection = db.collection('answers');
        collection.insertOne({ question: question, answer: response.data.choices[0].text }, function(err, result) {
          if (err) throw err;
          console.log('Answer saved to database');
          client.close();
        });
      }).catch(function(error) {
        console.error('OpenAI API error:', error);
        client.close();
      });
    });
  });
});