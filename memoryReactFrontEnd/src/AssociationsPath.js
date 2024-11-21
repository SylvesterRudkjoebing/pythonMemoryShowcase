import React, { useState } from "react";

const AssociationsPath = ({ associations, selectedPerson }) => {
  if (!associations || associations.length === 0) {
    return <p>No associations available to display.</p>;
  }

  const maxHeight = 500; // Max height for the SVG to prevent excessive scrolling
  const minCircleSpacing = 50; // Minimum space between circles
  const maxCircleSpacing = 80; // Maximum space between circles
  const nodeRadius = 30; // Radius for larger nodes
  const maxTextLength = 10; // Maximum length of the text

  // Determine the optimal circle spacing
  const circleSpacing = Math.max(
    minCircleSpacing,
    Math.min(maxCircleSpacing, maxHeight / (associations.length + 2))
  );

  const svgHeight = circleSpacing * (associations.length + 2); // Height based on the number of associations
  
  // Append the selectedPerson to the associations array at the end
  const fullAssociations = [...associations, selectedPerson];

  // Function to truncate text if it exceeds the max length
  const getTruncatedText = (text) => {
    if (text.length > maxTextLength) {
      return text.substring(0, maxTextLength) + "...";
    }
    return text;
  };

  return (
    <svg
      width="100%"
      height={svgHeight} // Dynamic height based on number of associations
      viewBox={`0 0 500 ${svgHeight}`} // Adjust viewBox to accommodate entire graph
      xmlns="http://www.w3.org/2000/svg"
      className="border border-gray-300"
    >
      {fullAssociations.map((assoc, index) => {
        // Determine the color based on the position (first and last node)
        const nodeColor =
          index === 0
            ? "#F87171" // Red for the first node
            : index === fullAssociations.length - 1
            ? "#34D399" // Green for the last node
            : "#4F46E5"; // Blue for other nodes

        // Set the first node to say "Dig" regardless of the actual association name
        const textToDisplay = index === 0 ? "Dig" : getTruncatedText(assoc.split(" ")[0]);

        return (
          <React.Fragment key={index}>
            <circle
              cx={250}
              cy={(index + 1) * circleSpacing}
              r={nodeRadius} // Increased radius for larger nodes
              fill={nodeColor} // Dynamic color based on position
              stroke="#000"
              strokeWidth="2"
            />
            <text
              x={250}
              y={(index + 1) * circleSpacing}
              textAnchor="middle"
              alignmentBaseline="middle"
              fill="#FFF"
              fontSize="12" // Adjust font size to fit
              fontWeight="bold"
              style={{ pointerEvents: "none" }}
            >
              {textToDisplay} {/* Display "Dig" for the first node */}
            </text>
            {index < fullAssociations.length - 1 && (
              <line
                x1={250}
                y1={(index + 1) * circleSpacing + nodeRadius}
                x2={250}
                y2={(index + 2) * circleSpacing - nodeRadius}
                stroke="#000"
                strokeWidth="2"
              />
            )}
          </React.Fragment>
        );
      })}
    </svg>
  );
};

export default AssociationsPath;
