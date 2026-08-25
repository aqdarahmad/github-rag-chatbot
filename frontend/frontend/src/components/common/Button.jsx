function Button({
  children,
  onClick,
  variant = "primary",
  type = "button",
  disabled = false,
}) {

  return (
    <button
      type={type}
      className={`button button-${variant}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
}

export default Button;