import "./globals.css";
import { ErrorBoundary } from "@/components/ErrorBoundary";

export const metadata = {
  title: "PDF to E-Course",
  description: "Turn any PDF into an interactive learning course",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <ErrorBoundary>{children}</ErrorBoundary>
      </body>
    </html>
  );
}
