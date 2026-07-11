import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [hardwareId, setHardwareId] = useState("");
  const [licenseStatus, setLicenseStatus] = useState("CHECKING");
  const [licenseFile, setLicenseFile] = useState(null);
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("Ready");
  
  // New States for Bay 2 & 3
  const [bay2Preview, setBay2Preview] = useState([]);
  const [bay3Preview, setBay3Preview] = useState([]);
  
  const [generatedPreview, setGeneratedPreview] = useState([]);
  //const [bay2, setBay2] = useState(5);
  //const [bay3, setBay3] = useState(3);
  const [generated, setGenerated] = useState(false);
  const [approved, setApproved] = useState(false);

  useEffect(() => { checkLicense(); }, []);

  const checkLicense = async () => {
    try {
        const res = await axios.get("http://127.0.0.1:8001/license-status");

        setLicenseStatus(res.data.status);

        if (res.data.hardware_id) {
            setHardwareId(res.data.hardware_id);
        }

    } catch {
        setLicenseStatus("NO_LICENSE");
    }
};

  const uploadLicense = async () => {
    if (!licenseFile) { alert("Select License File"); return; }
    const formData = new FormData();
    formData.append("file", licenseFile);
    try {
      const res = await axios.post("http://127.0.0.1:8001/upload-license", formData);
      if (res.data.status === "VALID") { alert("License Activated"); setLicenseStatus("VALID"); }
      else {
      console.log("Response:", res.data);
      alert(JSON.stringify(res.data, null, 2));
  }
    } catch (err) { alert(err.message); }
  };

  const previewFile = async () => {
    if (!file) { alert("Select Excel File"); return; }
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await axios.post("http://127.0.0.1:8001/preview", formData);
      setBay2Preview(res.data.bay2 || []);
      setBay3Preview(res.data.bay3 || []);
      setApproved(false);
      setGenerated(false);
    } catch (err) { alert(err.message); }
  };

  const generateScheduler = async () => {
    if (!file) { alert("Select Excel File"); return; }
    const formData = new FormData();
    formData.append("file", file);
    //formData.append("bay2", bay2);
    //formData.append("bay3", bay3);
    setStatus("Generating...");
    try {
  const res = await axios.post(
    "http://127.0.0.1:8001/generate",
    formData
  );

  console.log("Generate Response:", res.data);
  alert(JSON.stringify(res.data, null, 2));

  console.log("Generate Response:", res.data);

  alert(JSON.stringify(res.data, null, 2));

  setGeneratedPreview(res.data);
  setGenerated(true);
  setStatus("Generated");

} catch (error) {

  console.log(error.response);

  alert(JSON.stringify(error.response?.data, null, 2));

  setStatus("Error");
}
  };

  const downloadFile = () => { window.open("http://127.0.0.1:8001/download"); };

  if (licenseStatus === "CHECKING") return <h2>Checking License...</h2>;
  if (licenseStatus !== "VALID") {
  return (
    <div className="container">
      <div className="card">

        <h2>License Required</h2>

        <p><b>Hardware ID</b></p>

        <textarea
          value={hardwareId}
          readOnly
          rows={3}
          style={{
            width: "100%",
            marginBottom: "15px"
          }}
        />

        <input
          type="file"
          onChange={(e) => setLicenseFile(e.target.files[0])}
        />

        <br /><br />

        <button onClick={uploadLicense}>
          Browse License
        </button>

      </div>
    </div>
  );
}

  return (
    <div className="container">
      <div className="card">
        <h1>Plating Scheduler</h1>
        <div className="upload-section">
            <p>Upload Production Excel File</p>
            <input type="file" accept=".xlsx" onChange={(e) => setFile(e.target.files[0])} />
            <br/><br/>
            <button className="preview-btn" onClick={previewFile}>Preview</button>
        </div>

        {(bay2Preview.length > 0 || bay3Preview.length > 0) && (
          <>
            <h2 className="section-title">Scheduler Input Preview</h2>
            <div className="preview-tables-container">
              <div className="bay-table-wrapper">
                <h3>Bay 2 Preview</h3>
                <table>
                  <thead><tr><th>Part Number</th><th>Batches</th></tr></thead>
                  <tbody>
                    {bay2Preview.map((row, index) => (
                      <tr key={index}><td>{row["PART NUMBER"]}</td><td>{row["BATCHES"]}</td></tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <div className="bay-table-wrapper">
                <h3>Bay 3 Preview</h3>
                <table>
                  <thead><tr><th>Part Number</th><th>Batches</th></tr></thead>
                  <tbody>
                    {bay3Preview.map((row, index) => (
                      <tr key={index}><td>{row["PART NUMBER"]}</td><td>{row["BATCHES"]}</td></tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
            
            {/*<div className="bay-box">
                <div className="bay-item"><label>Bay 2 Tanks</label><input type="number" value={bay2} onChange={(e) => setBay2(e.target.value)} /></div>
                <div className="bay-item"><label>Bay 3 Tanks</label><input type="number" value={bay3} onChange={(e) => setBay3(e.target.value)} /></div>
            </div>*/}
            
            {!approved ? (
                <button className="okBtn" onClick={() => setApproved(true)}>Confirm Input</button>
            ) : (
                <button className="generate-btn" onClick={generateScheduler}>Generate Scheduler</button>
            )}
          </>
        )}

        {generated && (
          <div>
            <h2 className="section-title">Generated Scheduler</h2>
            <div className="table-container">
              <table>
                <thead><tr><th>Load</th><th>Part</th></tr></thead>
                <tbody>
                  {generatedPreview.map((row, index) => (
                    <tr key={index}><td>{row.Load}</td><td>{row.Part}</td></tr>
                  ))}
                </tbody>
              </table>
            </div>
            <br/>
            <button className="download-btn" onClick={downloadFile}>Download Excel</button>
          </div>
        )}
        
        <br/><br/>
        <div className="status">Status: {status}</div>
      </div>
    </div>
  );
}
export default App;