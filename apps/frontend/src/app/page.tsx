import LoginButton from "@/components/auth/login-button";
import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <main>
      <header className="w-full bg-zinc-700 p-4 flex justify-between items-center">
        <div className="text-xl font-bold">My App</div>
        <LoginButton>
          <Button variant="outline">ログイン</Button>
        </LoginButton>
      </header>
    </main>
  );
}
