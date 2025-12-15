
export const dynamic = 'force-dynamic';

export default function VersionPage() {
    return (
        <div style={{ padding: 40, backgroundColor: 'red', color: 'white', fontSize: 24, fontWeight: 'bold' }}>
            <h1>DEPLOYMENT DEBUG PAGE</h1>
            <p>Timestamp: {new Date().toISOString()}</p>
            <p>If you see this, the deployment is working.</p>
        </div>
    );
}
