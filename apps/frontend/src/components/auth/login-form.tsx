import CardWrapper from "@/components/auth/card-wrapper";

const LoginForm = () => {
  return (
    <CardWrapper
      headerLabel="Welcome back"
      backButtonLabel="アカウントを持っていませんか？"
      backButtonHref="/auth/register"
      showSocial
    >
      Login Form!
    </CardWrapper>
  );
};

export default LoginForm;
