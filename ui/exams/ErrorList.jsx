export default function ErrorList({ errors, onSelect }) {
  return (
    <div>
      <h3>Lỗi đề thi</h3>
      {errors.map((e, i) => (
        <div key={i}
             style={{ color: e.severity === "error" ? "red" : "orange" }}
             onClick={() => onSelect(e.index)}>
          [Q{e.question_id}] {e.message}
        </div>
      ))}
    </div>
  );
}
