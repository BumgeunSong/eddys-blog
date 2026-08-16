import KeystaticApp from './keystatic'

// This nested layout renders the Keystatic admin for every /keystatic route.
// It still inherits the root <html>/<body> from app/layout.tsx (required by the
// App Router); Keystatic renders its own full app shell inside <body>.
export default function KeystaticLayout() {
  return <KeystaticApp />
}
