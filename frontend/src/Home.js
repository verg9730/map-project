import { useState, useEffect } from "react";

function Home() {
  const [name, setName] = useState();

  useEffect(() => {
    const requestOptions = {
      method: 'GET',
      redirect: 'follow'
    };

    fetch("http://34.125.39.187.nip.io:8000/getuser", requestOptions)
      .then((response) => response.json())
      .then((json) =>{console.log(json); setName(json[0])})}
        ,[]);

  return (
    <div>
      {name}
    </div>
  );
}

export default Home;
