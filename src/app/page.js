export default async function Home() {
  const res = await fetch('http://localhost:5000/api/data', { cache: 'no-store' });
  const data = await res.json();

  return (
    <div>
      <h1>Next.js Frontend</h1>
      {data && <p>{data.message}</p>}
    </div>
  );
}
