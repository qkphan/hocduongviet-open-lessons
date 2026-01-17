import { useState } from "react";

export default function ExamEditor() {
  const [exam, setExam] = useState(null);
  const [errors, setErrors] = useState([]);

  const loadFile = async (file) => {
    const text = await file.text();
    setExam(JSON.parse(text));
  };

  const validateExam = async () => {
    const res = await fetch("/api/validate", {
      method: "POST",
      body: JSON.stringify(exam),
    });
    const data = await res.json();
    setErrors(data.errors || []);
  };

  return (
    <div>
      <h1>Exam Editor</h1>

      <input
        type="file"
        accept=".json"
        onChange={(e) => loadFile(e.target.files[0])}
      />

      <button onClick={validateExam}>Validate</button>

      {errors.length > 0 && (
        <ul>
          {errors.map((e, i) => (
            <li key={i}>
              {e.message} — {e.path.join(".")}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
