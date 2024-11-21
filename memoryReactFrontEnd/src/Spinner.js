import React from 'react';

const Spinner = () => (
  <div className="spinner">
    <style jsx>{`
      .spinner {
        display: inline-block;
        width: 50px;
        height: 50px;
        border: 3px solid rgba(0, 0, 0, 0.1);
        border-radius: 50%;
        border-top-color: #3498db;
        animation: spin 1s ease-in-out infinite;
      }
      @keyframes spin {
        to {
          transform: rotate(360deg);
        }
      }
    `}</style>
  </div>
);

export default Spinner;
