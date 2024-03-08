export type ResponceProps = {
  text: string;
};

export type ProgProps = {
  order: number;
  scene: number;
  click: () => void;
};

export function Progress({ order, scene, click }: ProgProps) {
  const handleClick: React.MouseEventHandler<HTMLButtonElement> = () => {
    click();
  };

  return (
    <div className="flex flex-wrap flex-col justify-around items-center h-screen bg-basecolor">
      <div>
        <div>scene={scene}</div>
        <div>order={order}</div>
        <button onClick={handleClick}>これたね～～～</button>
      </div>
    </div>
  );
}
