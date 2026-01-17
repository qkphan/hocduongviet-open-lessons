export default function QuestionEditor({ question, onChange }) {
  return (
    <textarea
      value={JSON.stringify(question, null, 2)}
      onChange={e => onChange(JSON.parse(e.target.value))}
      rows={20}
      cols={80}
    />
  );
}
