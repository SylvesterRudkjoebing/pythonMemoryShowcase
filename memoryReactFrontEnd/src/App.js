import React, { useState, useEffect } from "react";
import axios from "axios";
import AssociationsPath from "./AssociationsPath"; // Import the updated AssociationsPath component

function App() {
  const [people, setPeople] = useState([]);
  const [selectedPerson, setSelectedPerson] = useState("");
  const [associations, setAssociations] = useState([]);
  const [summary, setSummary] = useState(""); // Reset summary on new friend selection
  const [degrees, setDegrees] = useState(0); // Add degrees state
  const [loading, setLoading] = useState(false);
  const [hasClickedAssociate, setHasClickedAssociate] = useState(false); // Track if "Associer" was clicked

  // Set the base URL dynamically based on the environment
  const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

  useEffect(() => {
    axios
      .get(`${API_BASE_URL}/people/`)
      .then((response) => {
        setPeople(response.data.people);
      })
      .catch((error) => {
        console.error("There was an error fetching the people!", error);
      });
        // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Reset graph and summary when a new friend is selected
  const handleSelectPerson = (newPerson) => {
    setSelectedPerson(newPerson);
    setAssociations([]); // Clear associations to hide the graph
    setDegrees(0); // Reset degrees
    setHasClickedAssociate(false); // Mark as not associated yet
    setSummary(""); // Clear the summary
  };

  const handleCalculateAssociations = async () => {
    if (!selectedPerson) return;

    setLoading(true);
    setHasClickedAssociate(true); // Mark that the user has clicked "Associer"

    try {
      const response = await axios.post(
        `${API_BASE_URL}/calculate-associations/`,
        {
          target_name: selectedPerson,
        }
      );
      setDegrees(response.data.degrees); // Set the degrees value
      setAssociations(response.data.associations); // Set the associations data
      setSummary(""); // Clear the summary when recalculating
    } catch (error) {
      console.error("There was an error calculating the associations!", error);
      setAssociations([]);
      setDegrees(0);
    }

    setLoading(false);
  };

  const handleContextualizeAssociations = async () => {
    setLoading(true);

    try {
      const response = await axios.post(
        `${API_BASE_URL}/contextualize-associations/`,
        {
          associations: associations,
        }
      );
      setSummary(response.data.summary); // Set the summary data
    } catch (error) {
      console.error("There was an error summarizing the associations!", error);
      setSummary("");
    }

    setLoading(false);
  };

  return (
    <div className="App bg-gray-100 min-h-screen flex justify-center items-center pt-2 p-8">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full sm:max-w-xl lg:max-w-m">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-6">
          Hvordan blev du venner med...
        </h1>

        <div className="mb-4">
          <label
            htmlFor="personSelect"
            className="block text-lg text-gray-700 font-medium mb-2"
          >
            Vælg en ven:
          </label>
          <select
            id="personSelect"
            onChange={(e) => handleSelectPerson(e.target.value)} // Handle select person
            value={selectedPerson}
            className="w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {/* Only show the placeholder option when no person is selected */}
            <option value="" disabled={selectedPerson !== ""}>Venner</option>

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
          {loading ? "Associerer..." : "Associer"}
        </button>

        {/* Render AssociationsPath only after "Associer" is clicked */}
        {hasClickedAssociate && (
          <div className="mt-6">
            <AssociationsPath 
              associations={associations} 
              selectedPerson={selectedPerson} 
              degrees={degrees} 
            />
            {associations.length > 0 && (
              <button
                onClick={handleContextualizeAssociations}
                disabled={loading}
                className="w-full mt-4 p-3 bg-green-600 text-white font-semibold rounded-lg shadow-md hover:bg-green-700 disabled:opacity-50"
              >
                {loading ? "Husker..." : "Aktiver autobiografisk hukommelse"}
              </button>
            )}
          </div>
        )}

        {summary && (
          <div className="mt-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-2">
              Du husker nu, at:
            </h3>
            <p className="text-gray-700">{summary + "..."}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
