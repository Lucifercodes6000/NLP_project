import React, { useState } from 'react';
import axios from 'axios';
import { Graphviz } from 'graphviz-react';
import './index.css';

function App() {
    const [text, setText] = useState('If the light is red, stop.\nOtherwise, go.');
    const [file, setFile] = useState(null); // New state for file
    const [graphData, setGraphData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleFileChange = (e) => {
        if (e.target.files) {
            setFile(e.target.files[0]);
        }
    };

    const handleCompile = async () => {
        setLoading(true);
        setError(null);
        try {
            const formData = new FormData();
            if (file) {
                formData.append('file', file);
            } else {
                formData.append('text', text);
            }

            // Assuming backend is at localhost:8000
            const response = await axios.post('http://localhost:8000/compile', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setGraphData(response.data);
        } catch (err) {
            console.error(err);
            setError("Failed to compile. Ensure backend is running.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container">
            <header>
                <h1>FSM Compiler <span className="badge">v1.1</span></h1>
                <p>Transform technical manuals into Finite State Machines instantly.</p>
            </header>

            <main className="split-view">
                <section className="input-section">
                    <div className="card">
                        <h2>Manual Input</h2>

                        <div style={{ marginBottom: '1rem' }}>
                            <label style={{ display: 'block', marginBottom: '0.5rem', color: '#94a3b8', fontSize: '0.9rem' }}>Upload Text File</label>
                            <input type="file" accept=".txt" onChange={handleFileChange} style={{ color: '#f8fafc' }} />
                        </div>

                        <p style={{ textAlign: 'center', margin: '0.5rem 0', fontSize: '0.8rem' }}>- OR -</p>

                        <textarea
                            value={text}
                            onChange={(e) => { setText(e.target.value); setFile(null); }} // Clear file if text is edited
                            placeholder="Enter your manual steps here..."
                            disabled={!!file} // Disable text area if file is selected
                        />
                        <button onClick={handleCompile} disabled={loading} className="primary-btn">
                            {loading ? 'Compiling...' : 'Generate FSM'}
                        </button>
                        {error && <div className="error-msg">{error}</div>}
                    </div>
                </section>

                <section className="output-section">
                    <div className="card graph-card">
                        <h2>Visualization</h2>
                        <div className="graph-container">
                            {graphData ? (
                                <Graphviz dot={graphData.dot_source} options={{ zoom: true, fit: true }} />
                            ) : (
                                <div className="placeholder">
                                    FSM will appear here...
                                </div>
                            )}
                        </div>
                    </div>

                    {graphData && (
                        <div className="card stats-card">
                            <div className="stat">
                                <span className="label">States</span>
                                <span className="value">{graphData.fsm_stats.states}</span>
                            </div>
                            <div className="stat">
                                <span className="label">Transitions</span>
                                <span className="value">{graphData.fsm_stats.transitions}</span>
                            </div>
                        </div>
                    )}
                </section>
            </main>
        </div>
    );
}

export default App;
