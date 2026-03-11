import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import logo from "@/assets/logo.png";

const Login = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    navigate("/dashboard");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="w-full max-w-sm animate-fade-in">
        <div className="glass-card rounded-lg p-8 space-y-6">
          <div className="flex flex-col items-center gap-3">
            <img src={logo} alt="Feedback Agent" className="w-14 h-14 rounded-lg" />
            <h1 className="text-2xl font-semibold tracking-tight text-foreground">
              Feedback Agent
            </h1>
            <p className="text-sm text-muted-foreground">
              Análise inteligente de feedbacks
            </p>
          </div>

          <form onSubmit={handleLogin} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="seu@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="bg-secondary border-border"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Senha</Label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="bg-secondary border-border"
              />
            </div>
            <Button type="submit" className="w-full gradient-primary text-primary-foreground font-medium">
              Entrar
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;
