import React, { useState, useEffect } from 'react';

export const fetchData = async (url) => {
  url = "http://127.0.0.1:2637/api?input=" + url;
  console.log("Url = ", url)
  try {
    const response = await fetch(url, {
      method: 'GET', // or 'POST', 'PUT', etc., depending on your request
      headers: {
        'Accept': '*/*',
        'User-Agent': 'Thunder Client (https://www.thunderclient.com)',
      },
    });

    console.log("Api called", JSON.stringify(response))

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json(); // Parse the JSON from the response
    return data; // Return the data
  } catch (error) {
    console.error("Error fetching data:", error);
    return null; // Return null in case of an error
  }
};

export default function Result(props) {
  const [data, setData] = useState(null); // State to store the fetched data
  const [error, setError] = useState(null); // State to handle errors
  const [movieItems, setMovieItems] = useState([]);

  useEffect(() => {
    const fetchDataAsync = async () => {
      try {
        props.setLoading(true); // Set loading to true at the start
        const result = await fetchData(props.text); // Wait for the data to be fetched
        console.log(result);
        setData(result); // Set the data to state

        if (result && result.processed) {
          const processedData = JSON.parse(result.processed); // Parse the JSON string

          const items = [];
          Object.entries(processedData).forEach(([title, score]) => {
            items.push({ title, score });
          });
          setMovieItems(items);
        }
      } catch (err) {
        setError(err); // Handle any errors
      } finally {
        props.setLoading(false); // Set loading to false once data is fetched or error occurs
      }
    };

    fetchDataAsync();
  }, [props.text]); // Dependency array to ensure it runs when props.text changes

  // Conditional rendering based on state
  if (props.loading) {
    return <div>Loading...</div>; // Show loading indicator while waiting for data
  }

  if (error) {
    return <div>Error: {error.message}</div>; // Show error message if there's an error
  }

  return (
    <div>
      <h2>Results:</h2>
      {data ? (
        <div>
          {movieItems.map((item, index) => (
            <div key={index}>
              <strong>Title:</strong> {item.title}<br />
              <strong>Score:</strong> {item.score}<br />
            </div>
          ))}
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}
