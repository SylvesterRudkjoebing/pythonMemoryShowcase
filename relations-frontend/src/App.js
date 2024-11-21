import React, { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [people, setPeople] = useState([]);
  const [selectedPerson, setSelectedPerson] = useState("");
  const [associations, setAssociations] = useState([]);
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Fetch the list of people from the FastAPI backend
    axios.get("http://localhost:8000/people/")
      .then(response => {
        setPeople(response.data.people);  // Set the list of people
      })
      .catch(error => {
        console.error("There was an error fetching the people!", error);
      });
  }, []);

  const handleCalculateAssociations = async () => {
    if (!selectedPerson) return;

    setLoading(true);

    try {
      // Call the API to calculate associations
      const response = await axios.post("http://localhost:8000/calculate-associations/", {
        target_name: selectedPerson,
      });
      setAssociations(response.data.associations);  // Set the associations data
    } catch (error) {
      console.error("There was an error calculating the associations!", error);
    }

    setLoading(false);
  };

  const handleContextualizeAssociations = async () => {
    setLoading(true);

    try {
      // Call the API to summarize associations
      const response = await axios.post("http://localhost:8000/contextualize-associations/", {
        associations: associations,
      });
      setSummary(response.data.summary);  // Set the summary data
    } catch (error) {
      console.error("There was an error summarizing the associations!", error);
    }

    setLoading(false);
  };

  return (
    <div className="App bg-gray-100 min-h-screen flex justify-center items-center p-4">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full sm:w-96">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-6">
          Hvordan blev du venner med...
        </h1>

        <div className="mb-4">
          <label htmlFor="personSelect" className="block text-lg text-gray-700 font-medium mb-2">
            Vælg en ven:
          </label>
          <select
            id="personSelect"
            onChange={(e) => setSelectedPerson(e.target.value)}
            value={selectedPerson}
            className="w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value=""></option>
            {people.map((person, index) => (
              <option key={index} value={person}>
                {person}
              </option>
            ))}
          </select>
        </div>

        <button
          onClick={handleCalculateAssociations}
          disabled={loading}
          className="w-full mt-4 p-3 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "Calculating..." : "Calculate Associations"}
        </button>

        {associations.length > 0 && (
          <div className="mt-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-2">Associations:</h3>
            <ul className="list-disc pl-5">
              {associations.map((association, index) => (
                <li key={index} className="text-gray-700">{association}</li>
              ))}
            </ul>
          </div>
        )}

        {associations.length > 0 && (
          <button
            onClick={handleContextualizeAssociations}
            disabled={loading}
            className="w-full mt-6 p-3 bg-green-600 text-white font-semibold rounded-lg shadow-md hover:bg-green-700 disabled:opacity-50"
          >
            {loading ? "Summarizing..." : "Summarize Associations"}
          </button>
        )}

        {summary && (
          <div className="mt-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-2">Summary:</h3>
            <p className="text-gray-700">{summary}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
