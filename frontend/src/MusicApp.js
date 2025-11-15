import React, { useState } from "react";
import axios from "axios";

function MusicApp() {
  const [input, setInput] = useState("");
  const [emotion, setEmotion] = useState("");
  const [tracks, setTracks] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setEmotion("");
    setTracks([]);

    try {
      const response = await axios.post("http://localhost:8000/generate_music/", {
        text: input
      });

      setEmotion(response.data.emotion);
      setTracks(response.data.tracks);  // <-- Multiple files here
    } catch (err) {
      alert("Error generating music!");
      console.error(err);
    }

    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 600, margin: "2rem auto", fontFamily: "Arial" }}>
      <h2>Emotion-Based Music Generator</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          required
          style={{ width: "100%", padding: 10 }}
        />
        <button
          type="submit"
          disabled={loading}
          style={{
            marginTop: 10,
            padding: "10px 20px",
            background: "#0070f3",
            color: "white",
            border: "none",
            borderRadius: 4,
            cursor: "pointer"
          }}
        >
          {loading ? "Generating..." : "Generate Music"}
        </button>
      </form>

      {emotion && <p><strong>Detected Emotion:</strong> {emotion}</p>}

      {tracks.length > 0 && (
        <div>
          <h3>Choose a Music Track:</h3>

          {tracks.map((url, index) => (
            <div
              key={index}
              style={{
                marginBottom: "1.5rem",
                padding: "1rem",
                borderRadius: 8,
                border: "1px solid #ddd"
              }}
            >
              <p><strong>Option {index + 1}</strong></p>

              <audio controls src={url} style={{ width: "100%" }} />

              <a
                href={url}
                download={`track_${index + 1}.wav`}
                style={{ display: "block", marginTop: 8 }}
              >
                Download Track {index + 1}
              </a>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default MusicApp;
