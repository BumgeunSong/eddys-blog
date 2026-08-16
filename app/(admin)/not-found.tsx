import Link from 'next/link'

// Not-found boundary for the (admin) route group.
//
// Keystatic's admin app calls Next's notFound() by design for any URL its
// client router doesn't recognize (unknown collection/singleton, missing item,
// or a stray redirect target — e.g. a GitHub OAuth/created-app callback landing
// on an unexpected path). Splitting the app into route groups gave (admin) its
// own root layout with no not-found boundary, so those notFound() calls
// surfaced as a hard "Runtime NotFoundError" during SSR. This boundary catches
// them and renders a clean 404 with a way back into the CMS.
export default function AdminNotFound() {
  return (
    <main
      style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        gap: '0.75rem',
        fontFamily: 'system-ui, sans-serif',
        color: '#1f2937',
      }}
    >
      <h1 style={{ fontSize: '1.25rem', fontWeight: 600 }}>Page not found</h1>
      <p style={{ color: '#6b7280' }}>
        This CMS route doesn&apos;t exist.
      </p>
      <Link
        href="/keystatic"
        style={{ color: '#2563eb', textDecoration: 'underline' }}
      >
        Back to Keystatic
      </Link>
    </main>
  )
}
