
import { useState, useEffect } from "react";


function Feed() {

  return (
    <div>
        <form>
            <label>
                피드 내용:
                <input type="text" name="name" />
            </label>
            <input type="submit" value="Submit" />
        </form>
    </div>
  );
}

export default Feed;
